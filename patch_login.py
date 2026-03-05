import re

with open("kulup_paneli_yedekli_guncel (6).html", "r", encoding="utf-8") as f:
    content = f.read()

# CSS injection for login overlay
css_to_insert = """
    /* --- LOGIN OVERLAY --- */
    #loginOverlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
      z-index: 9999;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .login-container {
      background: white;
      padding: 40px;
      border-radius: 12px;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
      width: 100%;
      max-width: 400px;
      text-align: center;
    }
    .login-container h2 {
      margin-top: 0;
      margin-bottom: 24px;
      color: #1e293b;
      font-weight: 800;
      font-size: 24px;
    }
    .login-container .form-group {
      margin-bottom: 20px;
      text-align: left;
    }
    .login-container label {
      display: block;
      margin-bottom: 8px;
      font-weight: 600;
      color: #475569;
      font-size: 14px;
    }
    .login-container input {
      width: 100%;
      padding: 12px;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      font-size: 16px;
      transition: border-color 0.2s;
    }
    .login-container input:focus {
      outline: none;
      border-color: #3b82f6;
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    .login-container button {
      width: 100%;
      padding: 14px;
      background: #3b82f6;
      color: white;
      border: none;
      border-radius: 8px;
      font-size: 16px;
      font-weight: 700;
      cursor: pointer;
      transition: background 0.2s;
    }
    .login-container button:hover {
      background: #2563eb;
    }
    .login-error {
      color: #ef4444;
      font-size: 14px;
      margin-top: 12px;
      display: none;
    }

    /* Hide main app initially */
    #mainAppWrapper {
      display: none;
    }
"""

content = content.replace("</style>", css_to_insert + "\n</style>", 1)

html_to_insert = """
  <!-- LOGIN OVERLAY -->
  <div id="loginOverlay">
    <div class="login-container">
      <h2>Sisteme Giriş</h2>
      <div class="form-group">
        <label for="loginUsername">Kullanıcı Adı</label>
        <input type="text" id="loginUsername" placeholder="Kullanıcı Adı" autocomplete="off" />
      </div>
      <div class="form-group">
        <label for="loginPassword">Şifre</label>
        <input type="password" id="loginPassword" placeholder="Şifre" />
      </div>
      <button onclick="checkLogin()">Giriş Yap</button>
      <div id="loginError" class="login-error">Hatalı kullanıcı adı veya şifre!</div>
    </div>
  </div>

  <div id="mainAppWrapper">
"""

content = content.replace("<body>", "<body>\n" + html_to_insert, 1)

# close #mainAppWrapper just before </body>
content = content.replace("</body>", "  </div>\n</body>", 1)

js_to_insert = """
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

# inject JS logic after DOMContentLoaded block or just inside the <script> block
# <script>
content = content.replace("<script>", "<script>\n" + js_to_insert, 1)


with open("kulup_paneli_yedekli_guncel (6).html", "w", encoding="utf-8") as f:
    f.write(content)
