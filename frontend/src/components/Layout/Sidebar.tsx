import React from 'react'
import { NavLink } from 'react-router-dom'

export default function Sidebar() {
  return (
    <aside className="bg-white border-r w-64 transition-all">
      <div className="p-4">
        <h3 className="font-bold text-xl">RideSafe</h3>
      </div>
      <nav className="mt-6">
        <NavLink to="/" className="block px-4 py-2 hover:bg-slate-100">Dashboard</NavLink>
        <NavLink to="/profile" className="block px-4 py-2 hover:bg-slate-100">Profile</NavLink>
        <NavLink to="/documents" className="block px-4 py-2 hover:bg-slate-100">Documents</NavLink>
        <NavLink to="/qr" className="block px-4 py-2 hover:bg-slate-100">My QR</NavLink>
        <NavLink to="/notifications" className="block px-4 py-2 hover:bg-slate-100">Notifications</NavLink>
        <NavLink to="/audit" className="block px-4 py-2 hover:bg-slate-100">Audit</NavLink>
      </nav>
    </aside>
  )
}
