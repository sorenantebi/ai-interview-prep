import MyPage from "@/components/MyPage";
import { fileUrl, pageFiles, readChat, readPage } from "@/lib/page";

export const dynamic = "force-dynamic";

export default async function MyPageRoute() {
  const [html, files, chat] = await Promise.all([readPage(), pageFiles(), readChat()]);
  return <MyPage initialHtml={html} initialChat={chat} files={files.map((f) => ({ name: f, url: fileUrl(f) }))} />;
}
