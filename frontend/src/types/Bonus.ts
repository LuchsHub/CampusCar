export interface BonusGet extends Record<string, string | number | undefined> {
    id: string
    name: string
    cost: number
    count?: number
  }