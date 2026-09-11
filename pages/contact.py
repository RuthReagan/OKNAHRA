def render():
    return """
<section class="page-hero">
  <div class="container">
    <p class="breadcrumb"><a href="/index.html">Home</a> / Contact</p>
    <span class="eyebrow">Get in touch</span>
    <h1>Contact OKNAHRA</h1>
  </div>
</section>

<section>
  <div class="container" style="max-width:640px;">
    <form action="#" method="post" onsubmit="return false;">
      <div class="form-field">
        <label for="name">Name</label>
        <input id="name" name="name" type="text" required>
      </div>
      <div class="form-field">
        <label for="email">Email</label>
        <input id="email" name="email" type="email" required>
      </div>
      <div class="form-field">
        <label for="org">Organization (optional)</label>
        <input id="org" name="org" type="text">
      </div>
      <div class="form-field">
        <label for="message">Message</label>
        <textarea id="message" name="message" required></textarea>
      </div>
      <button class="btn btn-primary btn-block" type="submit">Send Message</button>
    </form>
  </div>
</section>
"""
