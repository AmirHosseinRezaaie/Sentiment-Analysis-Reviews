import test from 'node:test';
import assert from 'node:assert/strict';
import { predictDemoSentiment } from '../app/demo-predictor.mjs';

const defaults = {
  model: 'Logistic Regression',
  maxFeatures: 5000,
  testSize: 20,
  ngram: '2',
};

test('returns null for an empty review', () => {
  assert.equal(predictDemoSentiment({ ...defaults, text: '   ' }), null);
});

test('recognizes a clearly positive Persian demo review', () => {
  const result = predictDemoSentiment({ ...defaults, text: 'کیفیت عالی بود و خیلی راضی هستم' });
  assert.equal(result.sentiment, 'مثبت');
  assert.ok(result.confidence >= 54 && result.confidence <= 96);
});

test('recognizes a clearly negative Persian demo review', () => {
  const result = predictDemoSentiment({ ...defaults, text: 'کیفیت ضعیف و خراب بود و اصلا راضی نیستم' });
  assert.equal(result.sentiment, 'منفی');
});

test('explains when no known sentiment word is present', () => {
  const result = predictDemoSentiment({ ...defaults, text: 'امروز بسته به دستم رسید' });
  assert.match(result.reason, /واژه احساسی شناخته‌شده‌ای پیدا نشد/);
});

test('accepts the future Random Forest playground option', () => {
  const result = predictDemoSentiment({ ...defaults, model: 'RandomForest', text: 'این محصول عالی بود' });
  assert.match(result.reason, /جنگل تصادفی/);
});
