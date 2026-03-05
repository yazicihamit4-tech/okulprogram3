import re

file_path = "kulup_paneli_yedekli_guncel (6).html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

tfoot_search = r'(tfoot\.innerHTML = `\s*<tr>\s*<td colspan="2" style="padding:10px; text-align:right;">GENEL TOPLAM:</td>\s*<td style="padding:10px; text-align:right;">\$\{formatTL\(totalGross\)\}</td>\s*<td style="padding:10px; text-align:right; color:#ef4444;">-\$\{formatTL\(totalTax1\)\}</td>\s*<td style="padding:10px; text-align:right; color:#ef4444;">-\$\{formatTL\(totalTax2\)\}</td>\s*<td style="padding:10px; text-align:right; color:#10b981;">\$\{formatTL\(totalNet\)\}</td>\s*<td></td>\s*</tr>\s*`;)'

tfoot_replace = r'''tfoot.innerHTML = `
      <tr>
        <td colspan="2" style="padding:10px; text-align:right;">GENEL TOPLAM:</td>
        <td style="padding:10px; text-align:right;">${formatTL(totalGross)}</td>
        <td style="padding:10px; text-align:right; color:#ef4444;">-${formatTL(window.totalSgk)}</td>
        <td style="padding:10px; text-align:right; color:#ef4444;">-${formatTL(window.totalIsizlik)}</td>
        <td style="padding:10px; text-align:right; color:#ef4444;">-${formatTL(totalTax1)}</td>
        <td style="padding:10px; text-align:right; color:#ef4444;">-${formatTL(totalTax2)}</td>
        <td style="padding:10px; text-align:right; color:#10b981;">${formatTL(totalNet)}</td>
        <td></td>
      </tr>
    `;'''

content = re.sub(tfoot_search, tfoot_replace, content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
