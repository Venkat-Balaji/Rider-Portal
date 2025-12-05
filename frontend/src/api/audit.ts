import axios from './axios'
import { useQuery } from '@tanstack/react-query'

const fetchAudit = async () => {
  const { data } = await axios.get('/audit/')
  return data
}

export const useAudit = () => useQuery(['audit'], fetchAudit)
