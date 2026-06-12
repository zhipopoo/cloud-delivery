export interface CertificateItem {
  name: string
  category: string
  status: string
  issue_date: string
  expiry_date: string
  file_url: string
}

export interface LanguageLevel {
  cantonese: string
  english: string
  mandarin: string
}

export interface Member {
  id: number
  name: string
  avatar_seed: string
  role: string
  team: string
  title: string
  bio: string
  welink_id: string
  photo_url: string
  skills: string[]
  certificates: CertificateItem[]
  languages: LanguageLevel
  fans_count: number
}

export interface Project {
  id: number
  name: string
  client: string
  description: string
  start_date: string
  end_date: string
  status: string
}

export interface Assignment {
  id: number
  member_id: number
  member_name: string
  project_id: number
  project_name: string
  start: string
  end: string
  busy_level: string
  role_in_project: string
}

export interface FanMessage {
  id: number
  member_id: number
  author_name: string
  content: string
  created_at: string
}

export interface CalendarEvent {
  id: string
  title: string
  start: string
  end: string
  resourceId: string
  backgroundColor: string
  borderColor: string
  extendedProps: {
    busyLevel: string
    roleInProject: string
    projectName: string
  }
}

export interface UploadResult {
  filename: string
  url: string
  size: number
}
