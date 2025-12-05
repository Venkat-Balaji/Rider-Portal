import React from 'react'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import LoginPage from '@/pages/Login/LoginPage'
import DashboardPage from '@/pages/Dashboard/DashboardPage'
import ProfilePage from '@/pages/Profile/ProfilePage'
import DocumentsPage from '@/pages/Documents/DocumentsPage'
import QRPage from '@/pages/QR/QRPage'
import NotificationsPage from '@/pages/Notifications/NotificationsPage'
import AuditPage from '@/pages/Audit/AuditPage'
import RootLayout from '@/components/Layout/RootLayout'

const router = createBrowserRouter([
  { path: '/login', element: <LoginPage /> },
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
