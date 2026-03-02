export interface PageDTO {
  title: string;
  slug: string;
  content: string;
  updated_at: string;
}

export interface ArticleDTO {
  title: string;
  slug: string;
  summary: string;
  content: string;
  cover_image: string;
  youtube_video_id: string;
  show_in_gallery: boolean;
  published_at: string | null;
  updated_at: string;
}

export interface EventDTO {
  title: string;
  description: string;
  start_date: string;
  end_date: string;
  location: string;
  cover_image: string;
  youtube_video_id: string;
  show_in_gallery: boolean;
  updated_at: string;
}

export interface GalleryItemDTO {
  type: 'article' | 'event';
  title: string;
  slug?: string;
  cover_image: string;
  youtube_video_id: string;
}
