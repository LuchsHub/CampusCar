import { ref, onMounted, onUnmounted } from 'vue';

export const isKeyboardVisible = ref(false);

const MOBILE_BREAKPOINT = 768;
const KEYBOARD_HEIGHT_THRESHOLD = 150;

function isMobileDevice(): boolean {
  return window.innerWidth <= MOBILE_BREAKPOINT || 
         /Android|iPhone|iPad|iPod|Mobile|Windows Phone/i.test(navigator.userAgent);
}

export function useKeyboardVisible() {
  let initialViewportHeight = 0;
  let resizeTimeout: number | null = null;

  function onResize() {
    if (!window.visualViewport) return;
    if (resizeTimeout) {
      window.clearTimeout(resizeTimeout);
    }
    resizeTimeout = window.setTimeout(() => {
      const heightDiff = initialViewportHeight - window.visualViewport!.height;
      isKeyboardVisible.value = heightDiff > KEYBOARD_HEIGHT_THRESHOLD;
    }, 0); // Reduced delay for faster response
  }

  onMounted(() => {
    if (!isMobileDevice()) {
      isKeyboardVisible.value = false;
      return;
    }
    if (window.visualViewport) {
      initialViewportHeight = window.visualViewport.height;
      window.visualViewport.addEventListener('resize', onResize, { passive: true });
    }
    window.addEventListener('orientationchange', () => {
      setTimeout(() => {
        if (window.visualViewport) {
          initialViewportHeight = window.visualViewport.height;
        }
      }, 200);
    }, { passive: true });
  });

  onUnmounted(() => {
    if (window.visualViewport) {
      window.visualViewport.removeEventListener('resize', onResize);
    }
    if (resizeTimeout) {
      window.clearTimeout(resizeTimeout);
    }
  });
}