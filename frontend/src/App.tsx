import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { Layout } from './components/Layout';
import { AgendaPage } from './pages/AgendaPage';
import { ArticleDetailPage } from './pages/ArticleDetailPage';
import { ArticlesListPage } from './pages/ArticlesListPage';
import { GalleryPage } from './pages/GalleryPage';
import { PageBySlug } from './pages/PageBySlug';
import { PreviewArticlePage } from './pages/PreviewArticlePage';

export function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<PageBySlug slug="inicio" />} />
          <Route path="/agenda" element={<AgendaPage />} />
          <Route path="/galeria" element={<GalleryPage />} />
          <Route path="/artigos" element={<ArticlesListPage />} />
          <Route path="/artigos/:slug" element={<ArticleDetailPage />} />
          <Route path="/sobre" element={<PageBySlug slug="sobre" />} />
          <Route path="/contato" element={<PageBySlug slug="contato" />} />
          <Route path="/preview/artigos/:slug" element={<PreviewArticlePage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
