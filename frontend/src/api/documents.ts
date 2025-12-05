import axios from './axios'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

export type Document = {
  uuid: string
  name: string
  mime_type: string
  storage_path?: string
  thumbnail_path?: string
  created_at: string
}

const fetchDocs = async () => {
  const { data } = await axios.get('/documents/')
  return data as Document[]
}

export const useDocuments = () => useQuery(['documents'], fetchDocs)

export const useCreateDocumentMeta = () => {
  const qc = useQueryClient()
  return useMutation((meta: any) => axios.post('/documents/', meta), {
    onSuccess: () => qc.invalidateQueries(['documents'])
  })
}

export const useSignedUploadUrl = () =>
  useMutation((payload: { filename: string; content_type: string }) => axios.post('/documents/signed-url', payload))

export const useDeleteDocument = () => {
  const qc = useQueryClient()
  return useMutation((uuid: string) => axios.delete(`/documents/${uuid}/`), {
    onSuccess: () => qc.invalidateQueries(['documents'])
  })
}
