import re

with open("kulup_paneli_yedekli_guncel (6).html", "r", encoding="utf-8") as f:
    content = f.read()

# Let's fix the bug in my previous script where `addEventListener` could fail if the script is placed in the head
# and DOM hasn't loaded yet.
# Also `const user` is unused in JS, just a small clean up.

# Replace the injected JS logic
old_js = """
  // LOGIN LOGIC
  function checkLogin() {
    const user = document.getElementById('loginUsername').value.trim().toLowerCase();
    const pass = document.getElementById('loginPassword').value.trim();

    // Using string matching as requested: user "zübeydehanım", pass "715859"
    // Handle specific turkish characters if typed slightly differently, but "zübeydehanım" is exact target.
    // Replace 'I'/'i' properly to handle case sensitivity just in case
    let userNormalized = document.getElementById('loginUsername').value.trim().toLocaleLowerCase('tr-TR');

    if (userNormalized === 'zübeydehanım' && pass === '715859') {
      document.getElementById('loginOverlay').style.display = 'none';
      document.getElementById('mainAppWrapper').style.display = 'block';
      document.getElementById('loginError').style.display = 'none';
    } else {
      document.getElementById('loginError').style.display = 'block';
    }
  }

  // Handle enter key press on password
  document.getElementById('loginPassword').addEventListener('keypress', function (e) {
      if (e.key === 'Enter') {
          checkLogin();
      }
  });
"""

new_js = """
  // LOGIN LOGIC
  function checkLogin() {
    const userNormalized = document.getElementById('loginUsername').value.trim().toLocaleLowerCase('tr-TR');
    const pass = document.getElementById('loginPassword').value.trim();

    if (userNormalized === 'zübeydehanım' && pass === '715859') {
      document.getElementById('loginOverlay').style.display = 'none';
      document.getElementById('mainAppWrapper').style.display = 'block';
      document.getElementById('loginError').style.display = 'none';
    } else {
      document.getElementById('loginError').style.display = 'block';
    }
  }

  document.addEventListener('DOMContentLoaded', function() {
      // Setup login listener
      const loginPassEl = document.getElementById('loginPassword');
      if (loginPassEl) {
          loginPassEl.addEventListener('keypress', function (e) {
              if (e.key === 'Enter') {
                  checkLogin();
              }
          });
      }
  });
"""

if old_js in content:
    content = content.replace(old_js, new_js)
    with open("kulup_paneli_yedekli_guncel (6).html", "w", encoding="utf-8") as f:
        f.write(content)
    print("JS fixed successfully.")
else:
    print("Old JS block not found.")
