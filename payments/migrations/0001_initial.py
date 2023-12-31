# Generated by Django 4.2.8 on 2023-12-07 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("loans", "0001_initial"),
        ("customers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("external_id", models.CharField(max_length=60, unique=True)),
                ("total_amount", models.DecimalField(decimal_places=10, max_digits=20)),
                (
                    "status",
                    models.SmallIntegerField(
                        choices=[(1, "completed"), (2, "rejected")]
                    ),
                ),
                ("paid_at", models.DateTimeField()),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="customers.customer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PaymentDetail",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("amount", models.DecimalField(decimal_places=10, max_digits=20)),
                (
                    "loan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="loans.loan"
                    ),
                ),
                (
                    "payment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="payments.payment",
                    ),
                ),
            ],
        ),
    ]
