from django.db import models
from datetime import date


class NonDeleted(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)

    def all(self):
        return super().all().filter(deleted_at=None)


class SoftDelete(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)
    everything = models.Manager()
    objects = NonDeleted()

    def soft_deleted(self):
        self.deleted_at = date.today()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.deleted_at = date.today()
        self.save()

    class Meta:
        abstract = True


class Province(SoftDelete):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Province"
        verbose_name_plural = "Provinces"


class District(SoftDelete):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "District"
        verbose_name_plural = "Districts"


class SubDistrict(SoftDelete):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    district = models.ForeignKey(District, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sub-District"
        verbose_name_plural = "Sub-Districts"


class AddressModel(models.Model):
    sub_district = models.ForeignKey(SubDistrict, on_delete=models.RESTRICT)

    class Meta:
        abstract = True

    def __str__(self):
        return self.sub_district.name

    def get_full_address(self):
        return f"{self.sub_district.name}, {self.sub_district.district.name}, {self.sub_district.district.province.name} {self.sub_district.zipcode}"

    def get_full_address_en(self):
        return f"{self.sub_district.name_en}, {self.sub_district.district.name_en}, {self.sub_district.district.province.name_en} {self.sub_district.zipcode}"

    def get_district_name(self):
        return self.sub_district.district.name

    def get_province_name(self):
        return self.sub_district.district.province.name

    def get_zipcode(self):
        return self.sub_district.zipcode
