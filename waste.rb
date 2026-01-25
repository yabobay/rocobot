require_relative 'rosettacode.rb'

require 'cri'

waste = Cri::Command.define {
  name 'waste'

  flag :h, :help, 'show this help message' do |value, cmd|
    puts cmd.help
    exit
  end
}

waste.define_command('langs') {
  summary 'Show languages on RosettaCode'

  flag :r, :random, 'Display a random language'

  run do |opts, args, cmd|
    langs = RosettaCode::languages
    if opts[:random]
      puts langs.force.sample
      exit
    end
    langs.each { |i| puts i }
  end
}

ARGV.push '-h' if ARGV.empty?
waste.run(ARGV)
