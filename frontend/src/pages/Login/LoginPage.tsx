// src/pages/Login/LoginPage.tsx
import React, { useEffect, useState, useCallback } from 'react'
import { supabase } from '@/auth/supabaseClient'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'

/**
 * Login / SignUp combined page
 * - Full viewport centered split-screen
 * - Sliding overlay covers one whole panel (left or right)
 * - Mobile stacked layout
 * - After successful signin/signup we push a post-login history entry
 *   and add a popstate listener so "Back" returns to /login if user is signed-in.
 */

export default function LoginPage(): JSX.Element {
  const [isSignUp, setIsSignUp] = useState(false)
  const [loading, setLoading] = useState(false)
  const [form, setForm] = useState({ name: '', email: '', password: '' })
  const navigate = useNavigate()

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm((s) => ({ ...s, [e.target.name]: e.target.value }))

  // helper to detect signed-in state (exists token)
  const isSignedIn = useCallback(() => {
    const token = localStorage.getItem('riders:token') || ''
    return Boolean(token)
  }, [])

  // Handle browser back: if user is signed in and user presses back -> navigate to /login
  useEffect(() => {
    const onPop = (ev: PopStateEvent) => {
      // If user is signed in, send them back to the login page when they hit Back
      if (isSignedIn()) {
        navigate('/login', { replace: true })
      }
    }
    window.addEventListener('popstate', onPop)
    return () => window.removeEventListener('popstate', onPop)
  }, [isSignedIn, navigate])

  // Called after successful login/signup to add an extra history entry
  // so that pressing Back will reveal the login page (and our popstate handler will navigate)
  const pushPostLoginHistory = () => {
    try {
      // push a marker state so there's an entry to go "back" to
      window.history.pushState({ ridersPortal: 'post-login' }, '', window.location.pathname)
    } catch {
      /* ignore; history push might be blocked in some environments */
    }
  }

  const doSignIn = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email: form.email,
        password: form.password
      })
      if (error) throw error
      const token = (data.session as any)?.access_token
      if (token) localStorage.setItem('riders:token', token)
      toast.success('Signed in')
      // push a history marker so Back works as requested
      pushPostLoginHistory()
      navigate('/', { replace: false })
    } catch (err: any) {
      toast.error(err?.message || 'Sign in failed')
    } finally {
      setLoading(false)
    }
  }

  const doSignUp = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      const { error } = await supabase.auth.signUp({
        email: form.email,
        password: form.password,
        options: { data: { full_name: form.name } }
      })
      if (error) throw error
      toast.success('Sign up success — check your email if confirmation required')
      // Optionally auto-login depending on your Supabase settings; push history then navigate
      pushPostLoginHistory()
      navigate('/', { replace: false })
    } catch (err: any) {
      toast.error(err?.message || 'Sign up failed')
    } finally {
      setLoading(false)
    }
  }

  // Toggle helper used by overlay CTA buttons
  const toggleTo = (val: boolean) => setIsSignUp(val)

  return (
    <div className="min-h-screen w-full bg-slate-50 flex items-center justify-center p-6">
      <div className="relative w-full h-[90vh] max-w-7xl rounded-2xl shadow-2xl overflow-hidden bg-white">
        {/* Desktop two-column grid */}
        <div className="hidden md:grid md:grid-cols-2 h-full">
          {/* Left: Sign in */}
          <div className="flex items-center justify-center px-16">
            <div className="w-full max-w-lg">
              <h1 className="text-4xl font-extrabold mb-3">Sign in</h1>
              <p className="text-sm text-slate-500 mb-8">or use your account</p>

              <form onSubmit={doSignIn} className="space-y-6">
                <input
                  name="email"
                  type="email"
                  required
                  placeholder="Email"
                  value={form.email}
                  onChange={onChange}
                  className="w-full border rounded px-4 py-3 focus:outline-none focus:ring-2 focus:ring-red-300"
                />
                <input
                  name="password"
                  type="password"
                  required
                  placeholder="Password"
                  value={form.password}
                  onChange={onChange}
                  className="w-full border rounded px-4 py-3 focus:outline-none focus:ring-2 focus:ring-red-300"
                />

                <div className="flex items-center justify-between">
                  <div className="text-sm text-slate-600">Forgot your password?</div>
                  <div className="flex items-center gap-3">
                    <button
                      type="button"
                      onClick={() => toggleTo(true)}
                      className="px-4 py-2 rounded-full border border-slate-200"
                    >
                      SIGN UP
                    </button>
                    <button
                      type="submit"
                      disabled={loading}
                      className="px-6 py-2 rounded-full bg-red-500 text-white shadow"
                    >
                      {loading ? 'Signing...' : 'SIGN IN'}
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>

          {/* Right: Sign up */}
          <div className="flex items-center justify-center px-16">
            <div className="w-full max-w-lg">
              <h1 className="text-4xl font-extrabold mb-3">Create Account</h1>
              <p className="text-sm text-slate-500 mb-8">or use your email for registration</p>

              <form onSubmit={doSignUp} className="space-y-6">
                <input
                  name="name"
                  type="text"
                  required
                  placeholder="Name"
                  value={form.name}
                  onChange={onChange}
                  className="w-full border rounded px-4 py-3 focus:outline-none focus:ring-2 focus:ring-red-300"
                />
                <input
                  name="email"
                  type="email"
                  required
                  placeholder="Email"
                  value={form.email}
                  onChange={onChange}
                  className="w-full border rounded px-4 py-3 focus:outline-none focus:ring-2 focus:ring-red-300"
                />
                <input
                  name="password"
                  type="password"
                  required
                  placeholder="Password"
                  value={form.password}
                  onChange={onChange}
                  className="w-full border rounded px-4 py-3 focus:outline-none focus:ring-2 focus:ring-red-300"
                />

                <div className="flex items-center justify-between">
                  <button
                    type="submit"
                    disabled={loading}
                    className="px-6 py-2 rounded-full bg-white text-red-500 border shadow"
                  >
                    {loading ? 'Creating...' : 'SIGN UP'}
                  </button>
                  <button
                    type="button"
                    onClick={() => toggleTo(false)}
                    className="text-sm text-slate-600 underline"
                  >
                    Already have an account?
                  </button>
                </div>
              </form>
            </div>
          </div>

          {/* Sliding overlay: covers one entire panel at a time (w-1/2) */}
          <div
            className="absolute top-0 bottom-0 left-0 w-1/2 transition-transform duration-700 ease-in-out pointer-events-none"
            style={{
              // When signing up => overlay moves right-to-left covering left panel. When signed-in view (isSignUp=false) move to right so it covers right panel.
              transform: isSignUp ? 'translateX(0%)' : 'translateX(100%)'
            }}
          >
            <div className="h-full w-full rounded-none md:rounded-xl overflow-hidden shadow-xl">
              <div
                className="h-full w-full flex items-center justify-center text-white px-8"
                style={{
                  background:
                    'linear-gradient(135deg, #FF4B2B 0%, #FF416C 50%, #FF4B2B 100%)'
                }}
              >
                {!isSignUp ? (
                  <div className="text-center max-w-xs pointer-events-auto">
                    <h2 className="text-5xl font-extrabold tracking-tight mb-4">Welcome Back!</h2>
                    <p className="text-lg opacity-90 leading-relaxed mb-6">
                      To keep connected with us please login with your personal info
                    </p>
                    <button
                      onClick={() => toggleTo(true)}
                      className="px-8 py-3 rounded-full border border-white/40 hover:bg-white/10 transition text-lg font-medium"
                    >
                      SIGN UP
                    </button>
                  </div>
                ) : (
                  <div className="text-center max-w-xs pointer-events-auto">
                    <h2 className="text-5xl font-extrabold tracking-tight mb-4">Hello, Friend!</h2>
                    <p className="text-lg opacity-90 leading-relaxed mb-6">
                      Enter your personal details and start your journey with us
                    </p>
                    <button
                      onClick={() => toggleTo(false)}
                      className="px-8 py-3 rounded-full border border-white/40 hover:bg-white/10 transition text-lg font-medium"
                    >
                      SIGN IN
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Mobile stacked layout (md:hidden) */}
        <div className="md:hidden h-full grid grid-rows-[1fr_auto]">
          <div className="px-8 py-10 overflow-auto">
            {!isSignUp ? (
              <div className="max-w-md mx-auto">
                <h1 className="text-3xl font-extrabold mb-3">Sign in</h1>
                <p className="text-sm text-slate-500 mb-6">Use your email to sign in</p>
                <form onSubmit={doSignIn} className="space-y-4">
                  <input
                    name="email"
                    type="email"
                    required
                    placeholder="Email"
                    value={form.email}
                    onChange={onChange}
                    className="w-full border rounded px-4 py-3 focus:outline-none focus:ring-2 focus:ring-red-300"
                  />
                  <input
                    name="password"
                    type="password"
                    required
                    placeholder="Password"
                    value={form.password}
                    onChange={onChange}
                    className="w-full border rounded px-4 py-3 focus:outline-none focus:ring-2 focus:ring-red-300"
                  />
                  <div className="flex items-center justify-between">
                    <div className="text-sm text-slate-600">Forgot your password?</div>
                    <button
                      type="submit"
                      disabled={loading}
                      className="px-6 py-2 rounded-full bg-red-500 text-white"
                    >
                      {loading ? 'Signing...' : 'SIGN IN'}
                    </button>
                  </div>
                </form>
              </div>
            ) : (
              <div className="max-w-md mx-auto">
                <h1 className="text-3xl font-extrabold mb-3">Create Account</h1>
                <p className="text-sm text-slate-500 mb-6">Use your email for registration</p>
                <form onSubmit={doSignUp} className="space-y-4">
                  <input
                    name="name"
                    type="text"
                    required
                    placeholder="Name"
                    value={form.name}
                    onChange={onChange}
                    className="w-full border rounded px-4 py-3 focus:outline-none focus:ring-2 focus:ring-red-300"
                  />
                  <input
                    name="email"
                    type="email"
                    required
                    placeholder="Email"
                    value={form.email}
                    onChange={onChange}
                    className="w-full border rounded px-4 py-3 focus:outline-none focus:ring-2 focus:ring-red-300"
                  />
                  <input
                    name="password"
                    type="password"
                    required
                    placeholder="Password"
                    value={form.password}
                    onChange={onChange}
                    className="w-full border rounded px-4 py-3 focus:outline-none focus:ring-2 focus:ring-red-300"
                  />
                  <div className="flex items-center justify-between">
                    <button
                      type="submit"
                      disabled={loading}
                      className="px-6 py-2 rounded-full bg-white text-red-500 border"
                    >
                      {loading ? 'Creating...' : 'SIGN UP'}
                    </button>
                    <button type="button" onClick={() => toggleTo(false)} className="text-sm underline">
                      Already have an account?
                    </button>
                  </div>
                </form>
              </div>
            )}
          </div>

          {/* Mobile fixed bottom toggles */}
          <div className="px-6 py-4 border-t flex items-center justify-center gap-4">
            <button
              onClick={() => toggleTo(false)}
              className={`px-4 py-2 rounded-full ${!isSignUp ? 'bg-red-500 text-white' : 'bg-white text-slate-700'}`}
            >
              Sign in
            </button>
            <button
              onClick={() => toggleTo(true)}
              className={`px-4 py-2 rounded-full ${isSignUp ? 'bg-red-500 text-white' : 'bg-white text-slate-700'}`}
            >
              Sign up
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
