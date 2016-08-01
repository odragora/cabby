# coding=utf-8

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

import requests

from urlparse import urljoin

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.base import BaseTrigger

from apps.cabs.models import CabOrder, Cab, Passenger
from django.contrib.gis.geos import Point

import datetime
import random
import time
import os

__author__ = 'dragora'


class RandomSecondsTrigger(BaseTrigger):
    def __init__(self, sec_min, sec_max, *args, **kwargs):
        self.sec_min = sec_min
        self.sec_max = sec_max

    def get_next_fire_time(self, previous_fire_time, now):
        seconds = random.randint(self.sec_min, self.sec_max)
        return now + datetime.timedelta(seconds=seconds)


class Command(BaseCommand):
    help = 'Runs the realtime test of the project\'s functioning.\nTime measured in seconds.'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='URL of the web app')

        parser.add_argument('--map_min_x', type=float, default=30, help='x border value (min)')
        parser.add_argument('--map_max_x', type=float, default=31, help='x border value (max)')
        parser.add_argument('--map_min_y', type=float, default=-58, help='y border value (min)')
        parser.add_argument('--map_max_y', type=float, default=59, help='y border value (max)')

        parser.add_argument('--create_passengers', type=int, default=0, help='Create a passed number of passengers')
        parser.add_argument('--create_cabs', type=int, default=0, help='Create a passed number of cabs')

        parser.add_argument('cabs_update_frequency', type=int, help='Cabs data updating frequency')

        parser.add_argument('orders_create_basic_frequency_min', type=int, help='Order delay frequency (min)')
        parser.add_argument('orders_create_basic_frequency_max', type=int, help='Order delay frequency (max)')

        parser.add_argument(
            'orders_create_delayed_frequency_min', type=int, help='Delayed order creating frequency (min)')
        parser.add_argument(
            'orders_create_delayed_frequency_max', type=int, help='Delayed order creating frequency (max)')
        parser.add_argument(
            'orders_create_delayed_delay_min', type=int, help='Delayed order delay (min)')
        parser.add_argument(
            'orders_create_delayed_delay_max', type=int, help='Delayed order delay (max)')

        parser.add_argument('orders_cancel_frequency_min', type=int, help='Orders cancelling frequency (min)')
        parser.add_argument('orders_cancel_frequency_max', type=int, help='Orders cancelling frequency (min)')

    def write_info(self, msg, data=None, add_time=True):
        if not data:
            data = {}
        data['time'] = timezone.now()
        msg = '{time} ' + msg if add_time else msg
        self.stdout.write(msg.format(**data))

    def test_order_new_basic(self, base_url, min_x, max_x, min_y, max_y):
        self.write_info('Adding new basic cab order')
        request = requests.post(
            urljoin(base_url, '/api/orders/'),
            json={
                "pos_x": round(random.uniform(min_x, max_x), 11),
                "pos_y": round(random.uniform(min_y, max_y), 11),
                # Getting random passenger id from existing ones
                "passenger": Passenger.objects.order_by('?').first().id
            }
        )

    def test_order_new_delayed(self, base_url, min_x, max_x, min_y, max_y, delay_min, delay_max):
        self.write_info('Adding new delayed cab order')
        try:
            passenger = Passenger.objects.order_by('?').first()

            request = requests.post(
                urljoin(base_url, '/api/orders/'),
                json={
                    "pos_x": round(random.uniform(min_x, max_x), 11),
                    "pos_y": round(random.uniform(min_y, max_y), 11),
                    # Getting random passenger id from existing ones
                    "passenger": passenger.id,
                    "time": timezone.now() + datetime.timedelta(seconds=random.randint(delay_min, delay_max))
                }
            )
        except ObjectDoesNotExist:
            self.write_info('No passengers without an order left')

    def test_order_cancel(self, base_url):
        self.write_info('Canceling random cab order')
        # Getting random order id
        order_id = CabOrder.objects.order_by('?').first().id
        request = requests.delete(
            urljoin(base_url, '/api/orders/{id}'.format(order_id))
        )

    def test_cab_update(self, base_url, min_x, max_x, min_y, max_y):
        # Please note that the cabs are teleporting
        # The driving simulation is too complex for this task
        self.write_info('Updating cabs data')
        cabs = Cab.objects.all()
        for cab in cabs:
            request = requests.put(
                urljoin(base_url, '/api/cabs/{id}'.format(id=cab.id)),
                json={
                    "pos_x": round(random.uniform(min_x, max_x), 11),
                    "pos_y": round(random.uniform(min_y, max_y), 11),
                }
            )

    def test_create_passengers(self, amount):
        self.write_info('Creating test passengers')
        for i in range(amount):
            Passenger.objects.create(name='Emulated passenger')
        self.write_info(
            'Creating test passengers: DONE. Created: {amount}', {'amount': amount}
        )

    def test_create_cabs(self, amount, min_x, max_x, min_y, max_y):
        self.write_info('Creating test cabs')
        for i in range(amount):
            Cab.objects.create(
                position=Point(x=round(random.uniform(min_x, max_x), 11), y=round(random.uniform(min_y, max_y), 11))
            )
        self.write_info(
            'Creating test cab: DONE. Created: {amount}', {'amount': amount}
        )

    def handle(self, *args, **options):
        # Checking if args are valid
        if options['create_passengers'] < 0:
            raise CommandError(
                '--create_passengers option must be positive. Got value: {}'.format(options['create_passengers'])
            )
        if options['create_cabs'] < 0:
            raise CommandError(
                '--create_cabs option must be positive. Got value: {}'.format(options['create_cabs'])
            )
        # Preparing environment for emulating
        if options['create_passengers']:
            self.test_create_passengers(options['create_passengers'])
        if options['create_passengers']:
            self.test_create_cabs(
                options['create_cabs'],
                options['map_min_x'], options['map_max_x'], options['map_min_y'], options['map_max_y']
            )

        # Adding jobs to be executed periodically
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            self.test_order_new_basic,
            RandomSecondsTrigger(
                sec_min=options['orders_create_basic_frequency_min'],
                sec_max=options['orders_create_basic_frequency_max']
            ),
            kwargs={
                'base_url': options['url'],
                'min_x': options['map_min_x'],
                'max_x': options['map_max_x'],
                'min_y': options['map_min_y'],
                'max_y': options['map_max_y']
            }
        )
        scheduler.add_job(
            self.test_order_new_delayed,
            RandomSecondsTrigger(
                sec_min=options['orders_create_delayed_frequency_min'],
                sec_max=options['orders_create_delayed_frequency_max']
            ),
            kwargs={
                'base_url': options['url'],
                'min_x': options['map_min_x'],
                'max_x': options['map_max_x'],
                'min_y': options['map_min_y'],
                'max_y': options['map_max_y'],
                'delay_min': options['orders_create_delayed_delay_min'],
                'delay_max': options['orders_create_delayed_delay_max']
            }
        )
        scheduler.add_job(
            self.test_order_cancel,
            RandomSecondsTrigger(
                sec_min=options['orders_cancel_frequency_min'],
                sec_max=options['orders_cancel_frequency_max']
            ),
            kwargs={
                'base_url': options['url'],
            }
        )
        scheduler.add_job(
            self.test_cab_update, 'interval', seconds=options['cabs_update_frequency'],
            kwargs={
                'base_url': options['url'],
                'min_x': options['map_min_x'],
                'max_x': options['map_max_x'],
                'min_y': options['map_min_y'],
                'max_y': options['map_max_y']
            }
        )
        scheduler.start()

        self.stdout.write('...\nPress Ctrl+{0} to exit\n...'.format('Break' if os.name == 'nt' else 'C'))

        try:
            # Performing testing
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit,):
            # Stop testing
            self.stdout.write('\nCanceling emulation...')
            scheduler.shutdown()