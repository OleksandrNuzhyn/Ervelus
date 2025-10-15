import Toast, { createToastInterface } from "vue-toastification";
import "vue-toastification/dist/index.css";

const options = {
  position: "top-center",
  timeout: 7000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: false,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: true,
  hideProgressBar: true,
  closeButton: "button",
  icon: true,
  rtl: false,
  transition: "Vue-Toastification__fade",
  maxToasts: 5,
  newestOnTop: true
};

export const ToastPlugin = Toast;

export const toast = createToastInterface(options);

export const toastOptions = options;
