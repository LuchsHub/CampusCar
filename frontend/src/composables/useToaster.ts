import { createToaster } from "@meforma/vue-toaster";

const toaster = createToaster({
  duration: 2000,
  position: "top",
  maxToasts: 3,
});

export function useToaster() {
  const showToast = (type: "success" | "error" | "info", message: string) => {
    switch (type) {
      case "success":
        toaster.success(message);
        break;
      case "error":
        toaster.error(message);
        break;
      default:
        toaster.info(message);
    }
  };

  const showDefaultError = () => {
    toaster.error("Ein unbekannter Fehler ist aufgetreten.");
  };

  return {
    showToast,
    showDefaultError,
  };
}
