import axios from './axios'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

export type UserProfile = {
  id: string
  full_name: string
  phone: string
  dob?: string
  blood_group?: string
  allergies?: string
  medical_conditions?: string
  insurance?: string
  doctor_contact?: string
  emergency_contacts?: Array<{ name: string; phone: string }>
  profile_photo?: string
  profile_completion?: number
}

const fetchMe = async (): Promise<UserProfile> => {
  const { data } = await axios.get('/users/me/')
  return data
}

export const useMe = () => useQuery(['me'], fetchMe)

export const useUpdateMe = () => {
  const qc = useQueryClient()
  return useMutation((payload: Partial<UserProfile>) => axios.put('/users/me/', payload), {
    onSuccess: () => qc.invalidateQueries(['me'])
  })
}
