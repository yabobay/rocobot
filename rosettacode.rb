module RosettaCode
  require 'net/http'
  require 'sqlite3'
  require 'json'

  URL = 'rosettacode.org'

  @@http = nil
  at_exit { @@http.finish if @@http }

  @@db = SQLite3::Database.new File.expand_path('~/.rosettacode.db')
  @@db.execute <<-SQL
    CREATE TABLE IF NOT EXISTS pages (url TEXT NOT NULL, contents TEXT, time INTEGER, PRIMARY KEY (url))
  SQL

  def self.get_cached_page(url)
    r = @@db.execute 'SELECT contents, time FROM pages WHERE url=?', url
    return nil if r.empty? or Time.now.to_i - r[0][1] >= 86400
    raise Exception.new if r.length != 1 # ruby apparently has no assert, ok
    return r[0][0]
  end

  def self.put_cached_page(url, body)
    @@db.execute 'REPLACE INTO pages VALUES (?, ?, ?)', [url, body, Time.now.to_i]
  end

  def self.make_request(url, params)
    require 'stringio'
    res = StringIO.new
    res << url
    params.each_with_index do |x, i|
      res << (i == 0 ? '?' : '&')
      res << x[0] << '=' << x[1].gsub(' ', '_')
    end
    res.close
    return res.string
  end

  def self.send_request(req)
    url = URL + req
    page = get_cached_page(url)
    return page if page
    @@http ||= Net::HTTP.start(URL, :use_ssl => true)
    body = @@http.get(req).body
    put_cached_page(url, body)
    return body
  end

  def self.category_pages(category, type)
    # TODO: find out what cllimit and gcmlimit are
    params = { :format => 'json',
               :action => 'query',
               :generator => 'categorymembers',
               :gcmtitle => "Category:#{category}",
               :prop => 'categories',
               :cllimit => 'max',
               :gcmlimit => 'max' }
    pages = []
    res = nil
    begin
      req = make_request '/w/api.php', res ? params.merge(res['continue']) : params
      res = JSON.parse!(send_request(req))
      pages.append *res['query']['pages'].values.map { |x| x['title'] }
    end while res.key? 'continue'
    # mediawiki sends over a bunch of reduntant content (about 4X as
    # much as needed) but i did just what their documentation says so
    # i guess i can't do anything about it
    pages = pages.lazy.uniq
    case type
    when :pages
      pages = pages.select { |x| not x.start_with? /Category\:/i }
    when :categories
      pages = pages
        .select { |x| x.start_with? /Category\:/i }
        .map { |x| x.sub 'Category:', '' }
    else
      raise ArgumentError.new "Unknown page type #{type.inspect}"
    end
    return pages
  end

  def self.languages
    self.category_pages('Programming Languages', :categories)
  end
end
