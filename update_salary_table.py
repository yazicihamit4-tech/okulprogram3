import re

file_path = "kulup_paneli_yedekli_guncel (6).html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update table header
header_search = r'(<th style="padding:10px; background:#f8fafc; border-bottom:1px solid #e2e8f0; text-align:right;">Gelir V\. \(%15\)</th>\s*<th style="padding:10px; background:#f8fafc; border-bottom:1px solid #e2e8f0; text-align:right;">Damga V\. \(‰7\.59\)</th>)'
header_replace = r'<th style="padding:10px; background:#f8fafc; border-bottom:1px solid #e2e8f0; text-align:right;">SGK (%14)</th>\n            <th style="padding:10px; background:#f8fafc; border-bottom:1px solid #e2e8f0; text-align:right;">İşsizlik (%1)</th>\n            \1'

content = re.sub(header_search, header_replace, content)

# 2. Update logic for Kadir Şişman, Şebnem Şişman, and Hülya Pişkin
calc_search = r'(const tax1 = gross \* 0\.15; // Gelir Vergisi %15\s*const tax2 = gross \* 0\.00759; // Damga Vergisi binde 7\.59)'
calc_replace = r'''
      let sgk = 0;
      let isizlik = 0;
      let newGross = gross;
      const isSpecificPerson = ["Kadir Şişman", "Şebnem Şişman", "Hülya Pişkin"].includes(p.name);

      if (isSpecificPerson) {
        // SGK İşçi Payı %14
        sgk = gross * 0.14;
        // İşsizlik Sigortası İşçi Payı %1
        isizlik = gross * 0.01;
        // Net kazanç hesabı, matraha göre Gelir Vergisi falan vs ama biz brütü doğrudan ayırıyoruz veya ekliyoruz.
        // User requested adding calculation logic to the salary table for specific personnel
        // "Add SGK (%14) and İşsizlik (%1) columns and calculation logic to the salary table for specific personnel"
      }

      \1'''

content = re.sub(calc_search, calc_replace, content)

# 3. Update Net Calculation and totals
net_search = r'(const net = gross - tax1 - tax2 \+ exemption;\s*totalGross \+= gross;\s*totalTax1 \+= tax1;\s*totalTax2 \+= tax2;\s*totalNet \+= net;)'
net_replace = r'''const net = gross - tax1 - tax2 - sgk - isizlik + exemption;

      totalGross += gross;
      totalTax1 += tax1;
      totalTax2 += tax2;
      // You'd want totalSgk and totalIsizlik too. Let's add them globally or just locally if needed.
      window.totalSgk = (window.totalSgk || 0) + sgk;
      window.totalIsizlik = (window.totalIsizlik || 0) + isizlik;
      totalNet += net;'''

content = re.sub(net_search, net_replace, content)

# 4. Update the TR rendering
tr_search = r'(<td style="padding:10px; border-bottom:1px solid #e2e8f0; text-align:right;">\$\{formatTL\(gross\)\}</td>\s*<td style="padding:10px; border-bottom:1px solid #e2e8f0; text-align:right; color:#ef4444;">-\$\{formatTL\(tax1\)\}</td>)'
tr_replace = r'''<td style="padding:10px; border-bottom:1px solid #e2e8f0; text-align:right;">${formatTL(gross)}</td>
        <td style="padding:10px; border-bottom:1px solid #e2e8f0; text-align:right; color:#ef4444;">-${formatTL(sgk)}</td>
        <td style="padding:10px; border-bottom:1px solid #e2e8f0; text-align:right; color:#ef4444;">-${formatTL(isizlik)}</td>
        <td style="padding:10px; border-bottom:1px solid #e2e8f0; text-align:right; color:#ef4444;">-${formatTL(tax1)}</td>'''

content = re.sub(tr_search, tr_replace, content)

# 5. Initialize totals for SGK and Isizlik at the start of calculation
init_totals_search = r'(let totalGross = 0;\s*let totalTax1 = 0;\s*let totalTax2 = 0;\s*let totalNet = 0;)'
init_totals_replace = r'''\1
    window.totalSgk = 0;
    window.totalIsizlik = 0;'''

content = re.sub(init_totals_search, init_totals_replace, content)

# 6. Update Footer
tfoot_search = r'(<tr>\s*<td colspan="2" style="padding:12px 10px; text-align:right;">TOPLAM</td>\s*<td style="padding:12px 10px; text-align:right; color:#4f46e5;">\$\{formatTL\(totalGross\)\}</td>\s*<td style="padding:12px 10px; text-align:right; color:#ef4444;">-\$\{formatTL\(totalTax1\)\}</td>)'
tfoot_replace = r'''<tr>
          <td colspan="2" style="padding:12px 10px; text-align:right;">TOPLAM</td>
          <td style="padding:12px 10px; text-align:right; color:#4f46e5;">${formatTL(totalGross)}</td>
          <td style="padding:12px 10px; text-align:right; color:#ef4444;">-${formatTL(window.totalSgk)}</td>
          <td style="padding:12px 10px; text-align:right; color:#ef4444;">-${formatTL(window.totalIsizlik)}</td>
          <td style="padding:12px 10px; text-align:right; color:#ef4444;">-${formatTL(totalTax1)}</td>'''

content = re.sub(tfoot_search, tfoot_replace, content)

# 7. Update Excel Export
excel_search = r'("Brüt Ücret": Number\(gross\.toFixed\(2\)\),)'
excel_replace = r'''\1
          "SGK İşçi (%14)": Number(sgk.toFixed(2)),
          "İşsizlik İşçi (%1)": Number(isizlik.toFixed(2)),'''

content = re.sub(excel_search, excel_replace, content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
