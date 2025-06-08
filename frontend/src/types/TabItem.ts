import type { Component } from 'vue'

export interface TabItem {
    label: string
    to: string
    icon: Component
}