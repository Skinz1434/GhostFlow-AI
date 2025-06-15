import CookieConsent from 'react-cookie-consent'

export default function GDPRCookieConsent() {
  return (
    <CookieConsent
      location="bottom"
      buttonText="Accept all cookies"
      declineButtonText="Decline"
      enableDeclineButton
      cookieName="ghostflow_consent"
      onAccept={() => window.dataLayer?.push({ event: 'cookies_accepted' })}
      onDecline={() => window.dataLayer?.push({ event: 'cookies_declined' })}
      expires={150}
    >
      We value your privacy. Read our <a href="/privacy">Privacy Policy</a> and
      <a href="/terms"> Terms of Service</a> for more information.
    </CookieConsent>
  )
}
