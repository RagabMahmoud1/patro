# Delivery Report - Product Template View

## الوصف

هذا الـ module يوفر تقريرين بديلين لإيصال التوصيل:

### 1. **Delivery Slip (Product Template)** - إيصال بسيط
- يعرض **اسم المنتج الأساسي** (Product Template) بدلاً من المتغيرات
- مناسب للشركات التي لا تحتاج تفاصيل المتغيرات في إيصال التسليم
- يعرض معلومات المتغير كملاحظة صغيرة (إذا كان هناك أكثر من متغير)

### 2. **Delivery Slip (Grouped by Product)** - إيصال مجمّع
- يجمع كل المتغيرات حسب المنتج الأساسي
- يعرض **الكمية الإجمالية** لكل منتج
- يعرض تفاصيل المتغيرات تحت كل منتج (إذا كان هناك أكثر من متغير)

---

## التثبيت

### 1. من Terminal:

```bash
systemctl stop odoo

sudo -u postgres /opt/odoo/venv/bin/python3 /opt/odoo/odoo/odoo-bin \
  -c /etc/odoo.conf \
  -d patro_live \
  -i delivery_report_template \
  --stop-after-init

systemctl start odoo
```

### 2. من Odoo UI:

1. اذهب إلى **Apps**
2. احذف الفلتر "Apps" من البحث
3. ابحث عن `Delivery Report`
4. اضغط **Install**

---

## الاستخدام

### طباعة التقرير:

1. اذهب إلى **Inventory** → **Operations** → **Transfers**
2. افتح أي حركة مخزنية (Delivery Order / Receipt)
3. اضغط زر **Print** ▼
4. ستجد خيارين جديدين:
   - **Delivery Slip (Product Template)** - بسيط
   - **Delivery Slip (Grouped by Product)** - مجمّع

---

## مثال

### قبل (التقرير الافتراضي):
```
Product: T-Shirt - Red - S     Qty: 5
Product: T-Shirt - Red - M     Qty: 10
Product: T-Shirt - Blue - S    Qty: 3
Product: T-Shirt - Blue - M    Qty: 8
```

### بعد - التقرير البسيط:
```
Product: T-Shirt               Qty: 5
         (Red - S)
Product: T-Shirt               Qty: 10
         (Red - M)
Product: T-Shirt               Qty: 3
         (Blue - S)
Product: T-Shirt               Qty: 8
         (Blue - M)
```

### بعد - التقرير المجمّع:
```
Product: T-Shirt               Total: 26
  ↳ Red - S                    Qty: 5
  ↳ Red - M                    Qty: 10
  ↳ Blue - S                   Qty: 3
  ↳ Blue - M                   Qty: 8
```

---

## الميزات

✅ عرض المنتج الأساسي بدلاً من المتغيرات
✅ خيار التجميع حسب المنتج
✅ دعم اللغة العربية
✅ تصميم نظيف واحترافي
✅ مساحة للتوقيع
✅ معلومات العميل والعنوان

---

## التخصيص

إذا أردت تخصيص التقرير:

1. **تعديل القالب:**
   - الملف: `delivery_report_template/reports/delivery_report_template.xml`

2. **إضافة حقول جديدة:**
   - الملف: `delivery_report_template/models/stock_picking.py`
   - أضف methods جديدة في class `StockPicking`

3. **بعد التعديل:**
   ```bash
   systemctl restart odoo
   ```

---

## الدعم

لأي أسئلة أو مشاكل، تواصل مع فريق الدعم.

