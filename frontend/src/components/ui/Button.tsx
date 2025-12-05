import React from 'react'
export default function Button({ children, ...props }: any) {
  return (
    <button {...props} className={`px-4 py-2 rounded shadow ${props.className || ''}`}>
      {children}
    </button>
  )
}
