import axios from './axios'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

const fetchMyQR = async () => {
  const { data } = await axios.get('/qr/my/')
  return data
}

export const useMyQR = () => useQuery(['qr','mine'], fetchMyQR)

export const useRegenerateQR = () => {
  const qc = useQueryClient()
  return useMutation(() => axios.post('/users/me/qr/regenerate/'), {
    onSuccess: () => qc.invalidateQueries(['qr','mine'])
  })
}
