import { createI18n } from 'vue-i18n'

const messages = {
  en: {
    navigation: {
      dashboard: "Dashboard",
      gallery: "Gallery",
      profile: "Profile",
      terms: "Terms of Service",
      privacy: "Privacy Policy",
      refund: "Refund Policy",
      cookie: "Cookie Policy",
      coins: "Generations",
      rights_reserved: "All rights reserved",
      back: "Back",
      close: "Close"
    },
    workspace: {
      upload_click: "Select photo",
      style: "Style",
      choose_style: "Choose your style",
      final_result: "Final Result",
      transform_button: "Transform Photo",
      transforming: "Transforming...",
      error_invalid_type: "Invalid file type. Our magicians support only JPEG, PNG or WEBP format",
      error_file_size: "Maximum file size is 7 MB",
      error_failed_spell: "The spell has failed! Try casting the magic again",
      error_safety_rejected: "This dark magic was rejected by the safety system. Try another image",
      error_download: "Could not download the image. Please try again later",
      error_create_request: "Could not create request. Please try again later",
      error_timeout: "The generation request was cancelled because it took too long to complete",
      error_cancel_failed: "Could not cancel the generation request. It might have already been completed or cancelled",
      error_status_check: "An unexpected error occurred while checking generation status",
      error_file_not_found: "File for download not found. Please try again later",
      photo_tips_title: "Perfect Result Guide",
      photo_tips_subtitle: "For the best results, follow these recommendations",
      got_it: "Got it",
      tip_1_title: "Number of People:",
      tip_1_desc: "Ideally one person, maximum two for the most accurate results",
      tip_2_title: "Framing & Distance:",
      tip_2_desc: "The person should occupy most of the frame. Choose close-up portraits or full-body shots with minimal space above/below",
      tip_3_title: "Clarity:",
      tip_3_desc: "Faces must be sharp and clearly visible. Avoid blurry or low-resolution images",
      tip_4_title: "Lighting:",
      tip_4_desc: "Bright, even lighting without harsh shadows ensures a magical transformation",
      tip_5_title: "Background:",
      tip_5_desc: "Clean and simple backgrounds help the AI focus on the main subject"
    },
    gallery: {
      no_images: "No photos yet",
      no_images_desc: "Create your first AI art to see it here",
      go_dashboard: "Go to Dashboard",
      original: "Original",
      stylized: "Stylized",
      delete_title: "Delete Photos",
      delete_confirm: "Are you sure you want to delete these photos? All your photos are visible only to you and securely stored",
      confirm: "Confirm",
      error_load: "Failed to load gallery",
      error_delete: "Failed to delete photos",
      error_not_found: "These photos do not exist anymore",
      success_delete: "Photos deleted successfully",
      failed_input: "Failed to load input photo",
      failed_output: "Failed to load output photo",
      deleted_style: "Deleted Style",
      download: "Download",
      delete: "Delete",
      error_fetch: "An error occurred while fetching the photos",
      modal_error_not_found: "Request not found",
      error_download_failed: "Download failed",
      prev: "Prev",
      next: "Next"
    },
    profile: {
      promo_title: "Promo Code",
      promo_placeholder: "Enter code",
      promo_activate: "Activate",
      modal_cancel: "Cancel",
      modal_got_it: "Got it",
      alert_success: "Success",
      alert_promo_applied: "Promo code applied! You received {count} generations",
      alert_promo_error: "Promo Error",
      alert_promo_failed: "Failed to apply promo code. Please check the code and try again",
      support_title: "Support",
      support_desc: "Contact our team directly",
      delete_account: "Delete account",
      delete_account_confirm: "Are you sure you want to delete your account? All your data will be permanently removed",
      delete_account_error: "Currently unable to delete. Please contact support"
    },
    terms: {
      update_title: "Terms Update",
      update_desc: "We have updated our {types}. Please review and accept them to continue.",
      checkbox_label: "I have read and agree to the updated terms",
      accept_btn: "Accept and Continue",
      tos: "Terms of Service",
      privacy: "Privacy Policy",
      refund: "Refund Policy",
      cookies: "Cookie Policy",
      error_generic: "An unexpected error occurred",
      error_accept_failed: "An error occurred while accepting the terms. Please try again",
      error_unavailable: "The document is currently unavailable. Please try again later",
      and: "and"
    },
    maintenance: {
      title: "The site is under maintenance",
      message: "We'll be back soon. We apologize for the inconvenience",
      hint: "Please refresh the page periodically to check our status"
    },
    store: {
      title: "Store",
      free_bonuses: "Community Rewards",
      star_packages: "Star Packs",
      generations: "generations",
      premium_styles: "Lifetime access to all styles",
      invite_friend: "Invite friend",
      join_channel: "Join channel"
    }
  },
  uk: {
    navigation: {
      dashboard: "Майстерня",
      gallery: "Галерея",
      profile: "Профіль",
      terms: "Умови використання",
      privacy: "Конфіденційність",
      refund: "Політика повернення",
      cookie: "Політика Cookie",
      coins: "Генерації",
      rights_reserved: "Усі права захищені",
      back: "Назад",
      close: "Закрити"
    },
    workspace: {
      upload_click: "Оберіть фото",
      style: "Стиль",
      choose_style: "Оберіть стиль",
      final_result: "Результат",
      transform_button: "Перетворити фото",
      transforming: "Творимо магію...",
      error_invalid_type: "Невірний тип файлу. Наші маги підтримують лише JPEG, PNG або WEBP",
      error_file_size: "Максимальний розмір файлу — 7 МБ",
      error_failed_spell: "Заклинання не вдалося! Спробуйте ще раз",
      error_safety_rejected: "Ця темна магія була відхилена системою безпеки. Спробуйте інше фото",
      error_download: "Не вдалося завантажити фото. Спробуйте пізніше",
      error_create_request: "Не вдалося створити запит. Спробуйте пізніше",
      error_timeout: "Запит на генерацію було скасовано через перевищення часу очікування",
      error_cancel_failed: "Не вдалося скасувати запит. Можливо, він уже виконаний або скасований",
      error_status_check: "Сталася неочікувана помилка під час перевірки статусу генерації",
      error_file_not_found: "Файл для завантаження не знайдено. Спробуйте пізніше",
      photo_tips_title: "Секрет ідеального результату",
      photo_tips_subtitle: "Для найкращого результату дотримуйтесь цих рекомендацій",
      got_it: "Зрозуміло",
      tip_1_title: "Кількість людей:",
      tip_1_desc: "Ідеально одна людина, максимум дві для найкращого результату",
      tip_2_title: "Масштаб та відстань:",
      tip_2_desc: "Людина має займати більшу частину кадру. Обирайте портрети або фото в повний ріст з мінімальним простором навколо",
      tip_3_title: "Чіткість:",
      tip_3_desc: "Обличчя має бути чітким та добре освітленим. Уникайте розмитих або зернистих фото",
      tip_4_title: "Освітлення:",
      tip_4_desc: "Рівномірне світло без різких тіней гарантує найбільш якісну стилізацію",
      tip_5_title: "Фон:",
      tip_5_desc: "Простий фон без зайвих деталей допомагає ШІ краще обробити ваш образ"
    },
    gallery: {
      no_images: "Фото ще немає",
      no_images_desc: "Створіть свій перший ШІ-арт, щоб побачити його тут",
      go_dashboard: "До майстерні",
      original: "Оригінал",
      stylized: "Стилізація",
      delete_title: "Видалити фото",
      delete_confirm: "Ви точно хочете видалити ці фото? Ваші фото бачите лише ви. Вони надійно зберігаються",
      confirm: "Підтвердити",
      error_load: "Не вдалося завантажити галерею",
      error_delete: "Не вдалося видалити фото",
      error_not_found: "Ці фото більше не існують",
      success_delete: "Фото успішно видалено",
      failed_input: "Не вдалося завантажити вхідне фото",
      failed_output: "Не вдалося завантажити результат",
      deleted_style: "Видалений стиль",
      download: "Завантажити",
      delete: "Видалити",
      error_fetch: "Сталася помилка під час отримання фото",
      modal_error_not_found: "Запит не знайдено",
      error_download_failed: "Помилка завантаження",
      prev: "Назад",
      next: "Далі"
    },
    profile: {
      promo_title: "Промокод",
      promo_placeholder: "Введіть код",
      promo_activate: "Активувати",
      modal_cancel: "Скасувати",
      modal_got_it: "Зрозуміло",
      alert_success: "Успішно",
      alert_promo_applied: "Промокод активовано! Ви отримали {count} генерацій",
      alert_promo_error: "Помилка промокоду",
      alert_promo_failed: "Не вдалося активувати промокод. Перевірте код і спробуйте ще раз",
      support_title: "Підтримка",
      support_desc: "Прямий зв'язок з нашою командою",
      delete_account: "Видалити акаунт",
      delete_account_confirm: "Ви впевнені, що хочете видалити акаунт? Всі ваші дані будуть безповоротно видалені",
      delete_account_error: "Наразі неможливо видалити акаунт. Будь ласка, зверніться до підтримки"
    },
    terms: {
      update_title: "Оновлення умов",
      update_desc: "Ми оновили {types}. Перегляньте та прийміть їх для продовження.",
      checkbox_label: "Я прочитав(-ла) та погоджуюся з оновленими умовами",
      accept_btn: "Прийняти та продовжити",
      tos: "Умови використання",
      privacy: "Конфіденційність",
      refund: "Політика повернення",
      cookies: "Політика Cookie",
      error_generic: "Сталася неочікувана помилка",
      error_accept_failed: "Сталася помилка під час прийняття умов. Спробуйте ще раз",
      error_unavailable: "Документ наразі недоступний. Будь ласка, спробуйте пізніше",
      and: "та"
    },
    maintenance: {
      title: "Сайт на технічному обслуговуванні",
      message: "Ми скоро повернемося. Перепрошуємо за незручності",
      hint: "Будь ласка, періодично оновлюйте сторінку, щоб перевірити статус"
    },
    store: {
      title: "Магазин",
      free_bonuses: "Нагороди спільноти",
      star_packages: "Зіркові Паки",
      generations: "генерацій",
      premium_styles: "Довічний доступ до всіх стилів",
      invite_friend: "Запросити друга",
      join_channel: "Приєднатися до каналу"
    }
  }
}

function getDetectedLocale() {
  const tgLang = window.Telegram?.WebApp?.initDataUnsafe?.user?.language_code;
  const lang = (tgLang || navigator.language).toLowerCase();

  if (lang.startsWith('ru')) return 'uk';
  return Object.keys(messages).find(m => lang.startsWith(m)) || 'en';
}

const i18n = createI18n({
  legacy: false,
  globalInjection: true,
  locale: getDetectedLocale(),
  fallbackLocale: 'en',
  messages
})

export default i18n