export interface Page { title: string; slug: string; content: string; updated_at: string; }
export interface Article { title: string; slug: string; summary: string; content: string; cover_image: string; youtube_video_id?: string; published_at?: string; }
export interface Event { title: string; description: string; start_date: string; end_date: string; location: string; cover_image: string; youtube_video_id?: string; }
export interface GalleryItem { title: string; slug: string; type: string; cover_image: string; youtube_video_id?: string; }
