from django.db import models


class ContactMessage(models.Model):
    name = models.CharField("نام و نام خانوادگی", max_length=100)
    email = models.EmailField("ایمیل")
    subject = models.CharField("موضوع", max_length=200)
    message = models.TextField("متن پیام")
    is_read = models.BooleanField("خوانده شده", default=False)
    created_at = models.DateTimeField("تاریخ ارسال", auto_now_add=True)

    class Meta:
        verbose_name = "پیام تماس با ما"
        verbose_name_plural = "پیام‌های تماس با ما"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"