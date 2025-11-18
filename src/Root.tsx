import { Composition, staticFile } from 'remotion';
import { CaptionVideo } from './CaptionVideo';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="CaptionVideo"
        component={CaptionVideo}
        durationInFrames={6710}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          title: 'Vitajte v našom videu',
          subtitle: 'Toto je ukážka slovenských titulkov',
          backgroundColor: '#1a1a1a',
          textColor: '#ffffff',
          videoSrc: staticFile('assets/Guitar.mp4'),
        }}
      />
    </>
  );
};