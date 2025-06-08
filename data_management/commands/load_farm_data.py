import pandas as pd
from pathlib import Path
from django.core.management.base import BaseCommand
from api.models import Farm, SensorReading

class Command(BaseCommand):
    help = "Load merged_sensor_data.csv into SensorReading"

    def add_arguments(self, parser):
        parser.add_argument("--country", required=True)
        parser.add_argument("--farm", required=True)

    def handle(self, *args, **opts):
        country = opts["country"]
        farm_name = opts["farm"]
        csv_path = Path("data/processed") / country / "merged_sensor_data.csv"
        df = pd.read_csv(csv_path, parse_dates=["datetime"])

        farm, _ = Farm.objects.get_or_create(name=farm_name, country=country)

        bulk = [
            SensorReading(
                farm=farm,
                parameter=row.parameter,
                ts=row.datetime,
                value=row.value,
            )
            for row in df.itertuples()
        ]
        SensorReading.objects.bulk_create(bulk, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(f"Loaded {len(bulk)} rows for {farm}"))
