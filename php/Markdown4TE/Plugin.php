<?php
/**
 * Markdown plugin for typecho
 * 
 * @package Markdown
 * @author ichuan
 * @version 0.1
 * @link http://hi.baidu.com/ichuan
 */

class Markdown_Plugin implements Typecho_Plugin_Interface
{
    protected static $markdownify = null;

    public static function activate()
    {
        // replace richEditor
        Typecho_Plugin::factory('admin/write-post.php')->richEditor = array('Markdown_Plugin', 'render');
        Typecho_Plugin::factory('admin/write-page.php')->richEditor = array('Markdown_Plugin', 'render');
        // hook for markdown fiter
        Typecho_Plugin::factory('Widget_Contents_Post_Edit')->write = array('Markdown_Plugin', 'saveHook');
        Typecho_Plugin::factory('Widget_Contents_Page_Edit')->write = array('Markdown_Plugin', 'saveHook');
        Typecho_Plugin::factory('Widget_Abstract_Contents')->filter = array('Markdown_Plugin', 'loadHook');
    }

    public static function deactivate(){}

    public static function saveHook($contents, $obj)
    {
        require_once dirname(__FILE__) . '/markdown.php';
        $contents['text'] = Markdown($contents['text']);
        return $contents;
    }

    public static function strEndWith($str, $end)
    {
        return (strpos($str, $end) + strlen($end) == strlen($str));
    }

    public static function loadHook($contents, $obj)
    {
        $uri = @parse_url($_SERVER['REQUEST_URI']);
        if (is_array($uri) && (self::strEndWith($uri['path'], '/admin/write-post.php')) ||
                               self::strEndWith($uri['path'], '/admin/write-page.php')){
            require_once dirname(__FILE__) . '/markdownify/markdownify.php';
            if (is_null(self::$markdownify))
                self::$markdownify = new Markdownify;
            $contents['text'] = self::$markdownify->parseString($contents['text']);
        }
        return $contents;
    }

    public static function render()
    {
        $options = Helper::options();
        $js = Typecho_Common::url('Markdown/wmd/wmd.js', $options->pluginUrl);
        $preview = _t('预览');
        echo <<<EOF
<style type="text/css">
.markdownText {
font-family: "Panic Sans","Menlo","DejaVu Sans Mono","Helvetica Neue","Luxi Sans","DejaVu Sans",Tahoma,"Hiragino Sans GB",STHeiti !important;
font-size:14px !important;
}
.reset em{font-style:italic;color:#000;}
.reset ol{margin-left:10px;list-style:decimal inside none;}
.reset ul{margin-left:10px;list-style:square inside none;}
</style>
<script type="text/javascript">
var wmd_options = { autostart: false };
window.addEvent('domready', function() {
    var previewDiv = new Element('div', {id: 'previewDiv', class: 'reset markdownText', styles: {
            border: '1px solid gray',
            padding: '4px',
            'background-color': 'white'
        }}),
        p = new Element('p'),
        label = new Element('label', {class: 'typecho-label', for: 'previewDiv', text: '${preview}'}),
        textarea = $('text').addClass('markdownText');
        pp = textarea.getParent();
    previewDiv.inject(p);
    p.inject(pp, 'after');
    label.inject(pp, 'after');
    var previewManager = new Attacklab.wmd.previewManager({input: textarea, preview: previewDiv, output: null});
    var editor = new Attacklab.wmd.editor(textarea,previewManager.refresh);
});
</script>
<script type="text/javascript" src="${js}"></script>
EOF;
    }

    public static function config(Typecho_Widget_Helper_Form $form){}

    public static function personalConfig(Typecho_Widget_Helper_Form $form){}
}
