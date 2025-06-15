import { NextResponse, type NextRequest } from 'next/server'

export function middleware(req: NextRequest) {
  const res = NextResponse.next()

  res.headers.set(
    'Content-Security-Policy',
    "script-src 'self' 'unsafe-inline' *.googletagmanager.com"
  )

  res.headers.set(
    'X-FTC-Disclosure',
    'GhostFlow AI earns commissions on qualifying purchases.'
  )

  res.headers.set(
    'Set-Cookie',
    'Secure; HttpOnly; SameSite=Strict'
  )

  return res
}
