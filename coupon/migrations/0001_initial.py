# Generated by Django 4.1.5 on 2023-09-14 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('discount_value', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Discount')),
                ('discount_type', models.CharField(choices=[('first_buy', 'First Buy'), ('percentage', 'Percentage discount'), ('fixed', 'Fixed discount')], max_length=100, verbose_name='Discount type')),
                ('value_min', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Min. value')),
                ('code', models.CharField(max_length=200, unique=True, verbose_name='Code')),
                ('expiration_date', models.DateTimeField(verbose_name='Expiration date')),
                ('times_used', models.IntegerField(default=0, verbose_name='Times used')),
                ('max_times_used', models.IntegerField(verbose_name='Times used')),
                ('coupon_type', models.CharField(choices=[('not_general', 'Not general'), ('general', 'General')], max_length=100, verbose_name='Coupon type')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LogCoupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('total_value', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Total value')),
                ('total_discount', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Total discount')),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='coupon.coupon', verbose_name='Coupon')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]