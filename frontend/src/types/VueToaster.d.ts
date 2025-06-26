// This file is necessary since @meforma/vue-toaster does not contain typing information
declare module '@meforma/vue-toaster' {
    interface ToastOptions {
      duration?: number
      position?: string
      maxToasts?: number
    }
  
    export function createToaster(_options?: ToastOptions): {
      success: (_msg: string) => void
      error: (_msg: string) => void
      info: (_msg: string) => void
    }
  
    export default createToaster
  }
  