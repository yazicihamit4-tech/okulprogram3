import re

file_path = "kulup_paneli_yedekli_guncel (6).html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Current logic starts at around 1846:
# let sgk = 0;
# let isizlik = 0;
# let newGross = gross;
# const isSpecificPerson = ["Kadir Şişman", "Şebnem Şişman", "Hülya Pişkin"].includes(p.name);
#
# if (isSpecificPerson) {
#   // SGK İşçi Payı %14
#   sgk = gross * 0.14;
#   // İşsizlik Sigortası İşçi Payı %1
#   isizlik = gross * 0.01;
#   ...
# }
# const tax1 = gross * 0.15; // Gelir Vergisi %15

# New logic:
# If specific person: they want the net to remain the same as if there were no deductions.
# Let X be the new gross.
# New deductions based on X:
# sgk = X * 0.14
# isizlik = X * 0.01
# tax1 = X * 0.15
# tax2 = X * 0.00759
# Net = X - (X*0.14) - (X*0.01) - (X*0.15) - (X*0.00759)
# We want this Net to equal the old Net.
# old Net = gross - (gross*0.15) - (gross*0.00759) = gross * (1 - 0.15 - 0.00759) = gross * 0.84241
# New Net = X * (1 - 0.14 - 0.01 - 0.15 - 0.00759) = X * 0.69241
# So X = (gross * 0.84241) / 0.69241
# Let's adjust gross accordingly.

import re

file_path = "kulup_paneli_yedekli_guncel (6).html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

search_str = """
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

      const tax1 = gross * 0.15; // Gelir Vergisi %15
      const tax2 = gross * 0.00759; // Damga Vergisi binde 7.59

      let exemption = 0;
      if (p.role === "accounting") {
        exemption = gross * 0.0935; // Muhasebe personeli için %9.35 Vergi Muafiyeti
      }

      const net = gross - tax1 - tax2 - sgk - isizlik + exemption;
"""

replace_str = """
      let sgk = 0;
      let isizlik = 0;
      const isSpecificPerson = ["Kadir Şişman", "Şebnem Şişman", "Hülya Pişkin"].includes(p.name);

      if (isSpecificPerson) {
        // Kullanıcı bu 3 kişi için ellerine geçecek netin düşmemesini istedi.
        // Kesilecek tutar kadar brütlerini artırmamız gerekiyor.
        // Normal net: Brüt - (Brüt*0.15) - (Brüt*0.00759) = Brüt * 0.84241
        // Kesintili net: YeniBrüt - (YeniBrüt*0.14) - (YeniBrüt*0.01) - (YeniBrüt*0.15) - (YeniBrüt*0.00759) = YeniBrüt * 0.69241
        // Netin değişmemesi için: YeniBrüt * 0.69241 = Brüt * 0.84241 => YeniBrüt = Brüt * (0.84241 / 0.69241)
        gross = gross * (0.84241 / 0.69241);

        // Yeni brüt üzerinden SGK İşçi Payı %14
        sgk = gross * 0.14;
        // Yeni brüt üzerinden İşsizlik Sigortası İşçi Payı %1
        isizlik = gross * 0.01;
      }

      const tax1 = gross * 0.15; // Gelir Vergisi %15
      const tax2 = gross * 0.00759; // Damga Vergisi binde 7.59

      let exemption = 0;
      if (p.role === "accounting") {
        exemption = gross * 0.0935; // Muhasebe personeli için %9.35 Vergi Muafiyeti
      }

      const net = gross - tax1 - tax2 - sgk - isizlik + exemption;
"""

if search_str in content:
    content = content.replace(search_str, replace_str)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Replaced successfully.")
else:
    print("Search string not found.")
