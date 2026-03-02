import { Article, Event, GalleryItem, Page } from '../types/content';

const API_BASE = process.env.API_BASE_URL || 'http://localhost:8000/api';

async function getJSON<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) throw new Error('Falha ao carregar conteúdo');
  return response.json();
}

export const api = {
  page: (slug: string) => getJSON<Page>(`/public/pages/${slug}/`),
  articles: () => getJSON<Article[]>('/public/articles/'),
  article: (slug: string) => getJSON<Article>(`/public/articles/${slug}/`),
  events: () => getJSON<Event[]>('/public/events/'),
  gallery: () => getJSON<GalleryItem[]>('/public/gallery/'),
  previewArticle: (slug: string, token: string) => getJSON<Article>(`/preview/articles/${slug}/?token=${token}`),
};
