const positiveWords = ['عالی', 'خوب', 'عاشق', 'زیبا', 'راضی', 'پیشنهاد', 'سریع', 'کیفیت', 'دوست', 'بهترین', 'مفید', 'خوشحال', 'قیمت مناسب', 'عالیه'];
const negativeWords = ['بد', 'ضعیف', 'افتضاح', 'متأسفانه', 'ناراضی', 'خراب', 'کند', 'بی‌کیفیت', 'پشیمان', 'مشکل', 'دیر', 'اصلا', 'ناامید', 'گرون'];

const models = {
  'Logistic Regression': { title: 'رگرسیون لجستیک', positive: 1.12, negative: 1.05 },
  'Linear SVM': { title: 'ماشین بردار پشتیبان', positive: 1.2, negative: 1.14 },
  MultinomialNB: { title: 'بیز ساده چندجمله‌ای', positive: 0.96, negative: 1.08 },
  RandomForest: { title: 'جنگل تصادفی', positive: 1.05, negative: 1.02 },
};

/**
 * Browser-only interaction demo. This intentionally does not load the Python
 * pickle artifacts and must never be presented as a trained-model prediction.
 */
export function predictDemoSentiment({ text, model, maxFeatures, testSize, ngram }) {
  if (!text?.trim()) return null;

  const config = models[model] ?? models['Logistic Regression'];
  const normalized = text.toLowerCase();
  const positiveCount = positiveWords.reduce((count, word) => count + Number(normalized.includes(word)), 0);
  const negativeCount = negativeWords.reduce((count, word) => count + Number(normalized.includes(word)), 0);
  const score = (positiveCount * config.positive - negativeCount * config.negative)
    + (ngram === '3' ? 0.12 : ngram === '1' ? -0.08 : 0)
    + ((maxFeatures / 12000) - 0.4) * 0.12
    + (testSize - 20) * 0.002;
  const sentiment = score >= 0 ? 'مثبت' : 'منفی';
  const confidence = Math.min(96, Math.max(54, Math.round(56 + Math.abs(score) * 17 + Math.min(text.trim().split(/\s+/).length, 20) * 0.55)));
  const reason = positiveCount + negativeCount === 0
    ? 'واژه احساسی شناخته‌شده‌ای پیدا نشد؛ نتیجه با اطمینان پایین و بر اساس حالت پیش‌فرض نمایش داده شده است.'
    : `بر اساس ${positiveCount} نشانه مثبت و ${negativeCount} نشانه منفی در متن، ${config.title} این برچسب را پیشنهاد می‌کند.`;

  return { sentiment, confidence, reason };
}
