/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  basePath: process.env.GITHUB_ACTIONS ? '/Sentiment-Analysis-Reviews' : '',
  images: { unoptimized: true },
};

export default nextConfig;
