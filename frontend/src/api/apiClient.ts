import { ArticleDTO, EventDTO, GalleryItemDTO, PageDTO } from './types';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL ?? 'http://localhost:8000';

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`Erro HTTP ${response.status}`);
  }
  return (await response.json()) as T;
}

export const apiClient = {
  getPage: (slug: string) => request<PageDTO>(`/api/v1/public/pages/${slug}/`),
  getArticles: () => request<ArticleDTO[]>(`/api/v1/public/articles/`),
  getArticle: (slug: string) => request<ArticleDTO>(`/api/v1/public/articles/${slug}/`),
  getEvents: () => request<EventDTO[]>(`/api/v1/public/events/`),
  getGallery: () => request<GalleryItemDTO[]>(`/api/v1/public/gallery/`),
  getPreviewArticle: (slug: string, token: string) =>
    request<ArticleDTO>(`/api/v1/preview/articles/${slug}/?token=${encodeURIComponent(token)}`),
};
