import React from 'react'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { supabase } from '@/auth/supabaseClient'

export default function Navbar() {
  const navigate = useNavigate()
  const onLogout = async () => {
    await supabase.auth.signOut()
    localStorage.removeItem('riders:token')
    navigate('/login')
    toast.success('Logged out')
  }
  return (
    <header className="flex items-center justify-between p-4 border-b bg-white">
      <div className="text-lg font-medium">Rider Portal</div>
      <div className="flex items-center gap-3">
        <button onClick={onLogout} className="px-3 py-1 rounded bg-red-600 text-white">Logout</button>
      </div>
    </header>
  )
}
