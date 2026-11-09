import CopyEmailButton from '../components/CopyEmailButton.jsx'
import { TagList } from '../components/Tag.jsx'
import { contactTopics, links, profile } from '../content/site.js'
import './Contact.css'

/*
 * No backend yet: submitting opens the visitor's email app with the message prefilled.
 * Replace handleSubmit with an API call once a contact endpoint exists.
 */
function handleSubmit(event) {
  event.preventDefault()
  const data = new FormData(event.currentTarget)
  const name = data.get('name').trim()
  const email = data.get('email').trim()
  const subject = data.get('subject').trim()
  const message = data.get('message').trim()

  const body = `${message}\n\n— ${name} (${email})`
  const href = `mailto:${profile.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`
  window.location.href = href
}

export default function Contact() {
  const firstName = profile.name.split(' ')[0]

  return (
    <>
      <section className="container contact-head">
        <div className="page-head">
          <div className="page-head__title-group">
            <span className="eyebrow">/contact</span>
            <h1 className="page-head__title">Get in touch</h1>
          </div>
          <p className="page-head__lede">
            Interested in collaborating on AI, computer vision or web projects, or just want to say hi? Drop me a
            message.
          </p>
        </div>
      </section>

      <section className="container contact-body">
        <dl className="contact-info">
          <div className="contact-info__row">
            <dt>Status</dt>
            <dd className="contact-info__status">
              <span className="status-dot" aria-hidden="true" />
              {profile.status}
            </dd>
          </div>
          <div className="contact-info__row">
            <dt>Email</dt>
            <dd className="contact-info__email">
              <a href={`mailto:${profile.email}`}>{profile.email}</a>
              <CopyEmailButton email={profile.email} className="contact-copy-btn">
                Copy email
              </CopyEmailButton>
            </dd>
          </div>
          <div className="contact-info__row">
            <dt>Location</dt>
            <dd>
              {profile.location}
              <br />
              <span className="contact-info__sub">{profile.timezone}</span>
            </dd>
          </div>
          {(links.linkedin || links.github) && (
            <div className="contact-info__row">
              <dt>Social</dt>
              <dd className="contact-info__social">
                {links.linkedin && (
                  <a href={links.linkedin} target="_blank" rel="noreferrer">
                    LinkedIn profile ↗
                  </a>
                )}
                {links.github && (
                  <a href={links.github} target="_blank" rel="noreferrer">
                    GitHub ↗
                  </a>
                )}
              </dd>
            </div>
          )}
          <div className="contact-info__row contact-info__row--last">
            <dt>Good topics</dt>
            <dd className="contact-info__topics">
              <TagList items={contactTopics} />
            </dd>
          </div>
        </dl>

        <form className="contact-form" onSubmit={handleSubmit}>
          <div className="contact-form__pair">
            <div className="field">
              <label htmlFor="c-name">Name</label>
              <input id="c-name" name="name" type="text" autoComplete="name" placeholder="John Doe" required />
            </div>
            <div className="field">
              <label htmlFor="c-email">Email</label>
              <input
                id="c-email"
                name="email"
                type="email"
                autoComplete="email"
                placeholder="john@example.com"
                required
              />
            </div>
          </div>
          <div className="field">
            <label htmlFor="c-subject">Subject</label>
            <input id="c-subject" name="subject" type="text" placeholder="Collaboration on a RAG project" required />
          </div>
          <div className="field">
            <label htmlFor="c-msg">Message</label>
            <textarea
              id="c-msg"
              name="message"
              rows="6"
              placeholder={`Hello ${firstName}, I’d like to talk about…`}
              required
            />
          </div>
          <div className="contact-form__footer">
            <span className="contact-form__note">All fields are required. Sending opens your email app.</span>
            <button type="submit" className="btn btn--primary">
              Send message
            </button>
          </div>
        </form>
      </section>
    </>
  )
}
