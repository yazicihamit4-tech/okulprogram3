file_path = "kulup_paneli_yedekli_guncel (6).html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

search = r"""  function checkLogin\(\) \{
    const userNormalized = document\.getElementById\('loginUsername'\)\.value\.trim\(\)\.toLocaleLowerCase\('tr-TR'\);
    const pass = document\.getElementById\('loginPassword'\)\.value\.trim\(\);

    if \(userNormalized === 'zübeydehanım' && pass === '715859'\) \{
      document\.getElementById\('loginOverlay'\)\.style\.display = 'none';
      document\.getElementById\('mainAppWrapper'\)\.style\.display = 'block';
      document\.getElementById\('loginError'\)\.style\.display = 'none';
    \} else \{
      document\.getElementById\('loginError'\)\.style\.display = 'block';
    \}
  \}"""

replace = """  async function checkLogin() {
    const userNormalized = document.getElementById('loginUsername').value.trim().toLocaleLowerCase('tr-TR');
    const pass = document.getElementById('loginPassword').value.trim();

    // SHA-256 Hash of 715859 is 6ad04b02e45051fc74fec6748bc60bf26fb30fb7a202d6719ebd138287d2def8
    async function sha256(message) {
        const msgBuffer = new TextEncoder().encode(message);
        const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }

    let hashedPwd = "";
    if (pass !== "") {
        hashedPwd = await sha256(pass);
    }

    if (userNormalized === 'zübeydehanım' && hashedPwd === '6ad04b02e45051fc74fec6748bc60bf26fb30fb7a202d6719ebd138287d2def8') {
      document.getElementById('loginOverlay').style.display = 'none';
      document.getElementById('mainAppWrapper').style.display = 'block';
      document.getElementById('loginError').style.display = 'none';
    } else {
      document.getElementById('loginError').style.display = 'block';
    }
  }"""

new_content = re.sub(search, replace, content)

if content != new_content:
    print("Match found and replaced.")
else:
    print("No match found.")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
