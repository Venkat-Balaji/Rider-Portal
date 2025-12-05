import React, { useEffect } from 'react'
import { useMe, useUpdateMe } from '@/api/users'
import { z } from 'zod'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import toast from 'react-hot-toast'

const profileSchema = z.object({
  full_name: z.string().min(2),
  phone: z.string().optional(),
  dob: z.string().optional(),
  blood_group: z.string().optional(),
  allergies: z.string().optional(),
  medical_conditions: z.string().optional(),
  insurance: z.string().optional(),
  doctor_contact: z.string().optional()
})

type Form = z.infer<typeof profileSchema>

export default function ProfilePage() {
  const { data: me, isLoading } = useMe()
  const update = useUpdateMe()
  const { register, handleSubmit, reset } = useForm<Form>({ resolver: zodResolver(profileSchema) })

  useEffect(() => {
    if (me) reset(me)
  }, [me])

  const onSubmit = async (vals: Form) => {
    await update.mutateAsync(vals)
    toast.success('Profile saved')
  }

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Profile</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 max-w-2xl bg-white p-6 rounded shadow">
        <div>
          <label className="block text-sm">Full name</label>
          <input {...register('full_name')} className="w-full border px-3 py-2 rounded" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm">Phone</label>
            <input {...register('phone')} className="w-full border px-3 py-2 rounded" />
          </div>
          <div>
            <label className="block text-sm">Date of birth</label>
            <input type="date" {...register('dob')} className="w-full border px-3 py-2 rounded" />
          </div>
        </div>
        <div>
          <label className="block text-sm">Blood group</label>
          <input {...register('blood_group')} className="w-full border px-3 py-2 rounded" />
        </div>

        <div>
          <label className="block text-sm">Allergies</label>
          <textarea {...register('allergies')} className="w-full border px-3 py-2 rounded" />
        </div>

        <div className="flex gap-2">
          <button className="px-4 py-2 rounded bg-blue-600 text-white">Save</button>
          <button type="button" onClick={() => reset(me)} className="px-4 py-2 rounded border">Reset</button>
        </div>
      </form>
    </div>
  )
}
