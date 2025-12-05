import React from 'react'
import { useMe } from '@/api/users'
import { Link } from 'react-router-dom'

export default function DashboardPage() {
  const { data: user, isLoading } = useMe()
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Dashboard</h1>
        <div>Welcome{user ? `, ${user.full_name}` : ''}</div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-slate-500">Profile completion</div>
          <div className="text-3xl font-bold">{isLoading ? '—' : `${Math.round(user?.profile_completion ?? 0)}%`}</div>
          <Link to="/profile" className="mt-2 inline-block text-blue-600">Edit Profile</Link>
        </div>

        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-slate-500">Documents</div>
          <div className="text-3xl font-bold">—</div>
          <Link to="/documents" className="mt-2 inline-block text-blue-600">Manage documents</Link>
        </div>

        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-slate-500">QR Code</div>
          <div className="text-3xl font-bold">—</div>
          <Link to="/qr" className="mt-2 inline-block text-blue-600">View QR</Link>
        </div>
      </div>
    </div>
  )
}
