import axios from './axios'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

const fetchNotifications = async () => {
  const { data } = await axios.get('/notifications/')
  return data
}

export const useNotifications = () => useQuery(['notifications'], fetchNotifications)

export const useMarkAsRead = () => {
  const qc = useQueryClient()
  return useMutation((id: string) => axios.post(`/notifications/${id}/read/`), {
    onMutate: async (id) => {
      await qc.cancelQueries(['notifications'])
      const prev = qc.getQueryData(['notifications'])
      qc.setQueryData(['notifications'], (old: any) => {
        if (!old) return old
        return old.map((n: any) => (n.id === id ? { ...n, read: true } : n))
      })
      return { prev }
    },
    onError: (_err, _vars, context: any) => {
      if (context?.prev) qc.setQueryData(['notifications'], context.prev)
    },
    onSettled: () => qc.invalidateQueries(['notifications'])
  })
}
