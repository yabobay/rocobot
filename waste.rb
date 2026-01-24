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
  run do |opts, args, cmd|
    langs = RosettaCode::languages
    langs.each { |i| puts i}
  end
}

ARGV.push '-h' if ARGV.empty?
waste.run(ARGV)
