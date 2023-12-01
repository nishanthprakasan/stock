# Generated by Django 4.2.6 on 2023-10-20 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_transaction_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ltp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pc', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.companyprofile')),
            ],
        ),
    ]