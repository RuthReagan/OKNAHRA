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
    <form name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="/contact-thanks.html">
      <input type="hidden" name="form-name" value="contact">
      <p class="hidden" hidden>
        <label>Don't fill this out if you're human: <input name="bot-field"></label>
      </p>
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


def render_thanks():
    return """
<section class="page-hero">
  <div class="container">
    <p class="breadcrumb"><a href="/index.html">Home</a> / Contact</p>
    <span class="eyebrow">Message sent</span>
    <h1>Thanks &mdash; we'll be in touch</h1>
  </div>
</section>

<section>
  <div class="container" style="max-width:640px;">
    <p>Your message has been received. A member of the OKNAHRA board will follow up with you soon.</p>
    <a class="btn btn-primary" href="/index.html">Back to Home</a>
  </div>
</section>
"""
