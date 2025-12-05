import React, { useEffect } from 'react'
import { createBrowserRouter, RouterProvider, useNavigate } from 'react-router-dom'
import { supabase } from '@/auth/supabaseClient'
import LoginPage from '@/pages/Login/LoginPage'
import DashboardPage from '@/pages/Dashboard/DashboardPage'
import ProfilePage from '@/pages/Profile/ProfilePage'
import DocumentsPage from '@/pages/Documents/DocumentsPage'
import QRPage from '@/pages/QR/QRPage'
import NotificationsPage from '@/pages/Notifications/NotificationsPage'
import AuditPage from '@/pages/Audit/AuditPage'
import RootLayout from '@/components/Layout/RootLayout'

function PublicRoute({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate()
  useEffect(() => {
    const check = async () => {
      try {
        const { data } = await supabase.auth.getSession()
        const token = (data?.session as any)?.access_token || localStorage.getItem('riders:token')
        if (token) navigate('/', { replace: true })
      } catch (e) {
        // ignore
      }
    }
    check()
  }, [navigate])
  return <>{children}</>
}

const router = createBrowserRouter([
  { path: '/login', element: <PublicRoute><LoginPage /></PublicRoute> },
  {
    path: '/',
    element: <RootLayout />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: 'profile', element: <ProfilePage /> },
      { path: 'documents', element: <DocumentsPage /> },
      { path: 'qr', element: <QRPage /> },
      { path: 'notifications', element: <NotificationsPage /> },
      { path: 'audit', element: <AuditPage /> }
    ]
  }
])

export default function AppRouter() {
  return <RouterProvider router={router} />
}
