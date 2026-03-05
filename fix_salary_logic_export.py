import re

file_path = "kulup_paneli_yedekli_guncel (6).html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

search_str = """
        let sgk = 0;
        let isizlik = 0;
        const isSpecificPerson = ["Kadir Şişman", "Şebnem Şişman", "Hülya Pişkin"].includes(p.name);
        if (isSpecificPerson) {
          sgk = gross * 0.14;
          isizlik = gross * 0.01;
        }

        const tax1 = gross * 0.15;
        const tax2 = gross * 0.00759;

        let exemption = 0;
        if (p.role === "accounting") {
          exemption = gross * 0.0935;
        }

        const net = gross - tax1 - tax2 + exemption;
"""

replace_str = """
        let sgk = 0;
        let isizlik = 0;
        const isSpecificPerson = ["Kadir Şişman", "Şebnem Şişman", "Hülya Pişkin"].includes(p.name);
        if (isSpecificPerson) {
          gross = gross * (0.84241 / 0.69241);
          sgk = gross * 0.14;
          isizlik = gross * 0.01;
        }

        const tax1 = gross * 0.15;
        const tax2 = gross * 0.00759;

        let exemption = 0;
        if (p.role === "accounting") {
          exemption = gross * 0.0935;
        }

        const net = gross - tax1 - tax2 - sgk - isizlik + exemption;
"""

if search_str in content:
    content = content.replace(search_str, replace_str)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Replaced export successfully.")
else:
    print("Export search string not found.")
